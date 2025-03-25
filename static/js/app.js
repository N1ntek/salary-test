// Main JavaScript file for the Salary Calculator application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tabs
    const tabElements = document.querySelectorAll('button[data-bs-toggle="tab"]');
    tabElements.forEach(tabEl => {
        tabEl.addEventListener('shown.bs.tab', function (event) {
            // Load data when tab is shown
            const targetId = event.target.getAttribute('data-bs-target').substring(1);
            if (targetId === 'tax-rates') {
                loadTaxRates();
            } else if (targetId === 'exemptions') {
                loadExemptions();
            }
        });
    });

    // Load social fund rates for the dropdown
    loadSocialFundRates();

    // Set up form submission for salary calculation
    const salaryForm = document.getElementById('salary-form');
    if (salaryForm) {
        salaryForm.addEventListener('submit', function(event) {
            event.preventDefault();
            calculateSalary();
        });
    }

    // Load tax rates if tax rates tab is active initially
    if (document.querySelector('#tax-rates-tab').classList.contains('active')) {
        loadTaxRates();
    }

    // Load exemptions if exemptions tab is active initially
    if (document.querySelector('#exemptions-tab').classList.contains('active')) {
        loadExemptions();
    }
});

// Function to load social fund rates for the dropdown
async function loadSocialFundRates() {
    try {
        const response = await fetch('/api/v1/taxes/?tax_type=social_fund');
        if (!response.ok) {
            throw new Error('Failed to fetch social fund rates');
        }
        
        const rates = await response.json();
        const selectElement = document.getElementById('social-rate');
        
        // Clear existing options except the default one
        while (selectElement.options.length > 1) {
            selectElement.remove(1);
        }
        
        // Add options for each rate
        rates.forEach(rate => {
            const option = document.createElement('option');
            option.value = rate.id;
            option.textContent = `${rate.name} (${(rate.rate * 100).toFixed(2)}%)`;
            selectElement.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading social fund rates:', error);
    }
}

// Function to calculate salary
async function calculateSalary() {
    try {
        // Get form values
        const grossSalary = document.getElementById('gross-salary').value;
        const socialRateId = document.getElementById('social-rate').value;
        const customMedicalRate = document.getElementById('custom-medical-rate').value;
        const usePersonalExemption = document.getElementById('personal-exemption').checked;
        const useIncreasedPersonalExemption = document.getElementById('increased-personal-exemption').checked;
        const useSpouseExemption = document.getElementById('spouse-exemption').checked;
        const dependentCount = document.getElementById('dependent-count').value;
        const disabledDependentCount = document.getElementById('disabled-dependent-count').value;
        
        // Build query parameters
        let url = `/api/v1/salary/calculate?gross_salary=${grossSalary}`;
        
        if (socialRateId) {
            url += `&social_rate_id=${socialRateId}`;
        }
        
        if (customMedicalRate) {
            url += `&custom_medical_insurance_rate=${customMedicalRate}`;
        }
        
        if (usePersonalExemption) {
            url += '&use_personal_exemption=true';
        }
        
        if (useIncreasedPersonalExemption) {
            url += '&use_increased_personal_exemption=true';
        }
        
        if (useSpouseExemption) {
            url += '&use_increased_spouse_exemption=true';
        }
        
        if (dependentCount) {
            url += `&dependent_count=${dependentCount}`;
        }
        
        if (disabledDependentCount) {
            url += `&disabled_dependent_count=${disabledDependentCount}`;
        }
        
        // Make API request
        const response = await fetch(url, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to calculate salary');
        }
        
        const result = await response.json();
        
        // Display results
        document.getElementById('result-gross').textContent = formatCurrency(result.gross_salary);
        document.getElementById('result-social').textContent = formatCurrency(result.social_fund);
        document.getElementById('result-medical').textContent = formatCurrency(result.medical_insurance);
        document.getElementById('result-exemptions').textContent = formatCurrency(result.tax_exemptions);
        document.getElementById('result-income-tax').textContent = formatCurrency(result.income_tax);
        document.getElementById('result-net').textContent = formatCurrency(result.net_salary);
        document.getElementById('result-total').textContent = formatCurrency(result.total_salary);
        
        // Show results and hide placeholder
        document.getElementById('results').classList.remove('d-none');
        document.getElementById('no-results').classList.add('d-none');
    } catch (error) {
        console.error('Error calculating salary:', error);
        alert('Failed to calculate salary. Please check your inputs and try again.');
    }
}

// Function to load tax rates
async function loadTaxRates() {
    try {
        const response = await fetch('/api/v1/taxes/');
        if (!response.ok) {
            throw new Error('Failed to fetch tax rates');
        }
        
        const rates = await response.json();
        const tableBody = document.querySelector('#tax-rates-table tbody');
        tableBody.innerHTML = '';
        
        rates.forEach(rate => {
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${rate.name}</td>
                <td>${formatTaxType(rate.type)}</td>
                <td>${rate.code}</td>
                <td>${(rate.rate * 100).toFixed(2)}%</td>
                <td>${rate.description || ''}</td>
            `;
            
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading tax rates:', error);
    }
}

// Function to load exemptions
async function loadExemptions() {
    try {
        const response = await fetch('/api/v1/exemptions/');
        if (!response.ok) {
            throw new Error('Failed to fetch exemptions');
        }
        
        const exemptions = await response.json();
        const tableBody = document.querySelector('#exemptions-table tbody');
        tableBody.innerHTML = '';
        
        exemptions.forEach(exemption => {
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${exemption.name}</td>
                <td>${exemption.code}</td>
                <td>${formatCurrency(exemption.annual_amount)}</td>
                <td>${formatCurrency(exemption.monthly_amount)}</td>
                <td>${exemption.description || ''}</td>
            `;
            
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading exemptions:', error);
    }
}

// Helper function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('ro-MD', {
        style: 'currency',
        currency: 'MDL',
        minimumFractionDigits: 2
    }).format(amount);
}

// Helper function to format tax type
function formatTaxType(type) {
    switch (type) {
        case 'social_fund':
            return 'Social Fund';
        case 'medical_insurance':
            return 'Medical Insurance';
        case 'income_tax':
            return 'Income Tax';
        default:
            return type;
    }
}