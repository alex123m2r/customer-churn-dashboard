$(document).ready(function() {
    // Initialize datepickers for month and year selection
    $('#filter-month').datepicker({
        format: 'mm',
        viewMode: 'months',
        minViewMode: 'months',
        autoclose: true
    });
    $('#filter-year').datepicker({
        format: 'yyyy',
        viewMode: 'years',
        minViewMode: 'years',
        autoclose: true
    });

    // Toggle sidebar on mobile
    $('.navbar-toggler').click(function() {
        $('#sidebar').toggleClass('show');
    });

    // Close sidebar when clicking a link
    $('.sidebar .nav-link').click(function() {
        $('#sidebar').removeClass('show');
    });

    // Toggle chatbot visibility
    $('#chatbot-toggle').click(function() {
        $('#chatbot-section').slideToggle();
        $(this).toggleClass('active');
    });

    // Handle quick questions for chatbot
    $('.quick-question').click(function() {
        const question = $(this).data('question');
        sendChatMessage(question);
    });

    // Handle chat form submission
    $('#chat-submit').click(function() {
        const message = $('#chat-input').val().trim();
        if (message) {
            sendChatMessage(message);
        }
    });

    // Handle chat input Enter key
    $('#chat-input').keypress(function(e) {
        if (e.which === 13) {
            const message = $(this).val().trim();
            if (message) {
                sendChatMessage(message);
            }
        }
    });

    // Send chat message with typing effect
    function sendChatMessage(message) {
        $('#chatbot-messages').append(`
            <div class="chat-message user-message fade-in">${message}</div>
        `);
        $('#chat-input').val('');
        $('#chatbot-messages').scrollTop($('#chatbot-messages')[0].scrollHeight);

        // Get and validate current_revenue from input
        let currentRevenue = $('#currentRevenue').val().trim();
        console.log('Current Revenue Input:', currentRevenue); // Debug log
        if (!currentRevenue || isNaN(currentRevenue) || parseFloat(currentRevenue) <= 0) {
            currentRevenue = 0;
        } else {
            currentRevenue = parseFloat(currentRevenue);
        }

        $('#chatbot-messages').append(`
            <div class="chat-message typing-message fade-in" id="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        `);

        // Log payload for debugging
        const payload = { query: message, current_revenue: currentRevenue };
        console.log('Chat AJAX Payload:', payload);

        $.ajax({
            url: '/chat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function(response) {
                $('#typing-indicator').remove();
                const botResponse = response.response.replace(/\n/g, '<br>');
                typeMessage(botResponse);
            },
            error: function(xhr) {
                $('#typing-indicator').remove();
                $('#chatbot-messages').append(`
                    <div class="chat-message bot-message fade-in">
                        Sorry, I couldn't process your request. Please try again later.
                    </div>
                `);
                $('#chatbot-messages').scrollTop($('#chatbot-messages')[0].scrollHeight);
                console.error('Chatbot error:', xhr.responseText);
            }
        });
    }

    // Typing effect for bot response
    function typeMessage(message) {
        const messageDiv = $(`<div class="chat-message bot-message fade-in"></div>`);
        $('#chatbot-messages').append(messageDiv);
        let i = 0;
        const speed = 20;
        function type() {
            if (i < message.length) {
                const char = message.charAt(i);
                messageDiv.html(messageDiv.html() + (char === '<' ? message.slice(i, i + 4) : char));
                i += (char === '<' ? 4 : 1);
                $('#chatbot-messages').scrollTop($('#chatbot-messages')[0].scrollHeight);
                setTimeout(type, speed);
            }
        }
        type();
    }

    // Handle file upload and revenue input
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        const fileInput = document.getElementById('csvFile');
        const file = fileInput.files[0];
        let currentRevenue = $('#currentRevenue').val().trim();

        // Validate file input
        if (!file) {
            $('#upload-status').html(`
                <div class="alert alert-danger fade-in">
                    Please select a CSV file.
                </div>
            `);
            return;
        }

        if (!file.name.endsWith('.csv')) {
            $('#upload-status').html(`
                <div class="alert alert-danger fade-in">
                    Please upload a CSV file.
                </div>
            `);
            return;
        }

        // Validate and set currentRevenue
        if (!currentRevenue || isNaN(currentRevenue) || parseFloat(currentRevenue) <= 0) {
            currentRevenue = 0;
            $('#revenue-prediction').html(`
                <div class="alert alert-warning fade-in">
                    Current Revenue is 0
                </div>
            `);
        } else {
            currentRevenue = parseFloat(currentRevenue);
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('current_revenue', currentRevenue);

        $('#upload-status').html(`
            <div class="alert alert-info fade-in">
                <div class="loading">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="mt-2">Analyzing your data...</div>
            </div>
        `);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    $('#upload-status').html(`
                        <div class="alert alert-success fade-in">
                            Analysis complete! View insights below.
                        </div>
                    `);
                    // Show all sections
                    $('#data-summary-section').fadeIn();
                    $('#date-filter-section').fadeIn();
                    $('#chatbot-section').fadeIn();
                    $('#download-report-section').fadeIn();
                    $('#segmentation-section').fadeIn();
                    $('#retention-simulator-section').fadeIn();
                    $('#insights').fadeIn();

                    // Update summary metrics
                    $('#total-customers').text(response.data_info.rows);
                    $('#total-columns').text(response.data_info.columns);
                    $('#total-missing').text(response.data_info.missing_values);
                    $('#data-quality').text(response.data_info.data_quality_score.toFixed(2) + '%');

                    // Update insights
                    if (response.insights) {
                        $('#churn-rate').text((response.insights.churn_rate * 100).toFixed(2) + '%');
                        $('#model-accuracy').text((response.insights.model_accuracy * 100).toFixed(2) + '%');
                        if (response.insights.potential_monthly_loss !== null) {
                            $('#monthly-loss').text('₹' + response.insights.potential_monthly_loss.toFixed(2));
                            $('#yearly-loss').text('₹' + response.insights.potential_yearly_loss.toFixed(2));
                        } else {
                            $('#monthly-loss').text('₹0.00');
                            $('#yearly-loss').text('₹0.00');
                        }
                        updateCharts(response.charts);
                    }

                    // Predict revenue if provided
                    if (currentRevenue > 0) {
                        $.ajax({
                            url: '/predict_revenue',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({ current_revenue: currentRevenue }),
                            success: function(revResponse) {
                                if (revResponse.success) {
                                    $('#revenue-prediction').html(`
                                        <div class="alert alert-info fade-in">
                                            Predicted Revenue Impact:<br>
                                            Monthly Loss: ₹${revResponse.monthly_loss.toFixed(2)}<br>
                                            Annual Loss: ₹${revResponse.yearly_loss.toFixed(2)}<br>
                                            Future Revenue: ₹${revResponse.future_revenue.toFixed(2)}
                                        </div>
                                    `);
                                } else {
                                    $('#revenue-prediction').html(`
                                        <div class="alert alert-danger fade-in">
                                            ${revResponse.error}
                                        </div>
                                    `);
                                }
                            },
                            error: function(xhr) {
                                $('#revenue-prediction').html(`
                                    <div class="alert alert-danger fade-in">
                                        Error predicting revenue. Please try again.
                                    </div>
                                `);
                                console.error('Revenue prediction error:', xhr.responseText);
                            }
                        });
                    }

                    // Populate segmentation
                    if (response.data_info.column_names.includes('contract')) {
                        $.ajax({
                            url: '/chat',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({ query: 'Which customer segment has the highest churn?' }),
                            success: function(segResponse) {
                                $('#segmentation-content').html(`
                                    <div class="alert alert-info fade-in">
                                        ${segResponse.response.replace(/\n/g, '<br>')}
                                    </div>
                                `);
                            },
                            error: function(xhr) {
                                $('#segmentation-content').html(`
                                    <div class="alert alert-danger fade-in">
                                        Error fetching segmentation data.
                                    </div>
                                `);
                                console.error('Segmentation error:', xhr.responseText);
                            }
                        });
                    }
                } else {
                    $('#upload-status').html(`
                        <div class="alert alert-danger fade-in">
                            ${response.error || 'Analysis failed. Please check your data.'}
                        </div>
                    `);
                    if (response.warning) {
                        $('#insights-warnings').append(`
                            <div class="alert alert-warning fade-in">
                                ${response.warning}
                            </div>
                        `);
                        $('#insights').fadeIn();
                    }
                }
            },
            error: function(xhr) {
                $('#upload-status').html(`
                    <div class="alert alert-danger fade-in">
                        Server error. Please ensure the server is running and try again.
                    </div>
                `);
                console.error('File upload error:', xhr.responseText);
            }
        });
    });

    // Handle date filter submission
    $('#dateFilterForm').submit(function(e) {
        e.preventDefault();
        const month = $('#filter-month').val();
        const year = $('#filter-year').val();

        // Validate date inputs
        if (!month || !year) {
            $('#upload-status').html(`
                <div class="alert alert-danger fade-in">
                    Please select both month and year.
                </div>
            `);
            return;
        }

        $('#upload-status').html(`
            <div class="alert alert-info fade-in">
                <div class="loading">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="mt-2">Applying date filter...</div>
            </div>
        `);

        $.ajax({
            url: '/filter_by_date',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ month: month, year: year }),
            success: function(response) {
                if (response.success) {
                    $('#upload-status').html(`
                        <div class="alert alert-success fade-in">
                            Date filter applied successfully!
                        </div>
                    `);
                    $('#total-customers').text(response.data_info.rows);
                    $('#total-columns').text(response.data_info.columns);
                    $('#total-missing').text(response.data_info.missing_values);
                    $('#data-quality').text(response.data_info.data_quality_score.toFixed(2) + '%');

                    if (response.insights) {
                        $('#churn-rate').text((response.insights.churn_rate * 100).toFixed(2) + '%');
                        $('#model-accuracy').text((response.insights.model_accuracy * 100).toFixed(2) + '%');
                        if (response.insights.potential_monthly_loss !== null) {
                            $('#monthly-loss').text('₹' + response.insights.potential_monthly_loss.toFixed(2));
                            $('#yearly-loss').text('₹' + response.insights.potential_yearly_loss.toFixed(2));
                        } else {
                            $('#monthly-loss').text('₹0.00');
                            $('#yearly-loss').text('₹0.00');
                        }
                        updateCharts(response.charts);
                    }
                    $('#insights').fadeIn();
                } else {
                    $('#upload-status').html(`
                        <div class="alert alert-danger fade-in">
                            ${response.error || 'Failed to apply date filter.'}
                        </div>
                    `);
                }
            },
            error: function(xhr) {
                $('#upload-status').html(`
                    <div class="alert alert-danger fade-in">
                        Error applying date filter. Please try again.
                    </div>
                `);
                console.error('Date filter error:', xhr.responseText);
            }
        });
    });

    // Handle retention strategy simulator
    $('#retentionSimulatorForm').submit(function(e) {
        e.preventDefault();
        const churnReduction = $('#churn-reduction').val();
        let currentRevenue = $('#currentRevenue').val().trim();

        // Validate churn reduction input
        if (!churnReduction || isNaN(churnReduction) || churnReduction < 0 || churnReduction > 100) {
            $('#retention-result').html(`
                <div class="alert alert-danger fade-in">
                    Please enter a valid percentage (0-100).
                </div>
            `);
            return;
        }

        // Validate and set currentRevenue
        if (!currentRevenue || isNaN(currentRevenue) || parseFloat(currentRevenue) <= 0) {
            currentRevenue = 0;
            $('#retention-result').html(`
                <div class="alert alert-warning fade-in">
                    Current Revenue is 0, no loss predicted.
                </div>
            `);
            return;
        } else {
            currentRevenue = parseFloat(currentRevenue);
        }

        $('#retention-result').html(`
            <div class="alert alert-info fade-in">
                <div class="loading">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="mt-2">Simulating retention strategy...</div>
            </div>
        `);

        // Simulate impact by reducing churn rate
        $.ajax({
            url: '/predict_revenue',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ current_revenue: currentRevenue }),
            success: function(response) {
                if (response.success) {
                    const reducedChurnRate = response.monthly_loss * (1 - churnReduction / 100);
                    const reducedYearlyLoss = reducedChurnRate * 12;
                    $('#retention-result').html(`
                        <div class="alert alert-success fade-in">
                            With ${churnReduction}% churn reduction:<br>
                            Monthly Loss: ₹${reducedChurnRate.toFixed(2)}<br>
                            Annual Loss: ₹${reducedYearlyLoss.toFixed(2)}
                        </div>
                    `);
                } else {
                    $('#retention-result').html(`
                        <div class="alert alert-danger fade-in">
                            ${response.error}
                        </div>
                    `);
                }
            },
            error: function(xhr) {
                $('#retention-result').html(`
                    <div class="alert alert-danger fade-in">
                        Error simulating retention strategy.
                    </div>
                `);
                console.error('Retention simulator error:', xhr.responseText);
            }
        });
    });

    // Update charts and verify visibility
    function updateCharts(charts) {
        const chartIds = [
            'churn-distribution', 'tenure-chart', 'charges-chart',
            'contract-chart', 'feature-importance-chart', 'churn-over-time'
        ];
        chartIds.forEach(id => {
            const container = $(`#${id}`);
            const chartKey = id === 'churn-distribution' ? 'churn_distribution' :
                            id === 'tenure-chart' ? 'tenure_vs_churn' :
                            id === 'charges-chart' ? 'charges_vs_churn' :
                            id === 'contract-chart' ? 'contract_vs_churn' :
                            id === 'feature-importance-chart' ? 'feature_importance' :
                            'churn_over_time';
            
            if (charts && charts[chartKey]) {
                const imgSrc = `data:image/png;base64,${charts[chartKey]}`;
                container.html(`
                    <img src="${imgSrc}" class="img-fluid fade-in" alt="${id.replace('-', ' ')}">
                `);
                // Verify image load
                container.find('img').on('error', function() {
                    console.error(`Failed to load chart: ${id}`);
                    container.html(`
                        <div class="alert alert-warning fade-in">
                            Error loading chart. Please try again.
                        </div>
                    `);
                });
            } else {
                console.warn(`Chart data missing for ${id}`);
                container.html(`
                    <div class="alert alert-warning fade-in">
                        Chart data unavailable for ${id.replace('-', ' ')}.
                    </div>
                `);
            }
        });
        $('#insights').fadeIn();
    }

    // Back to top button visibility
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('#back-to-top').addClass('show');
        } else {
            $('#back-to-top').removeClass('show');
        }
    });

    // Smooth scroll for back to top
    $('#back-to-top').click(function(e) {
        e.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, 600);
    });
});