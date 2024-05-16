function addDropdown() {
    const dropdownContainer = document.querySelector('.search-form');
    const dropdownCount = dropdownContainer.querySelectorAll('.dropdown').length;

    if (dropdownCount >= 5) {
        alert('You cannot add more than 4 dropdowns.');
        return;
    }

    const newDropdown = document.createElement('div');
    newDropdown.classList.add('dropdown');
    newDropdown.innerHTML = `
        <label for="dropdown_${dropdownCount + 1}">Fund Name ${dropdownCount}:</label>
        <select id="dropdown_${dropdownCount + 1}">
            <option value="">Select Fund Name</option>
        </select>
    `;

    // Get the element before which to insert the new dropdown
    const targetElement = document.getElementById(`btn-search`);

    if (targetElement && targetElement.parentNode === dropdownContainer) {
        // If the target element exists and is a child of dropdownContainer, insert before it
        dropdownContainer.insertBefore(newDropdown, targetElement);
    } else {
        // If the target element does not exist or is not a child of dropdownContainer, append to the end
        dropdownContainer.appendChild(newDropdown);
    }

    // Populate the newly added dropdown with the same data as the fund_name dropdown
    populateNewDropdown(dropdownCount + 1);

    // Enable the remove dropdown button
    const removeButton = document.getElementById('btn-remove-dropdown');
    if (removeButton) {
        removeButton.disabled = false;
    }
}

function populateNewDropdown(newDropdownIndex) {
    // Get the data from the fund_name dropdown
    const fundNameDropdown = document.getElementById('fund_name');
    const selectedValue = fundNameDropdown.value;
    const options = fundNameDropdown.querySelectorAll('option');

    // Populate options in the newly added dropdown, excluding the selected option
    const newDropdown = document.getElementById(`dropdown_${newDropdownIndex}`);
    newDropdown.innerHTML = ''; // Clear existing options

    options.forEach(option => {
        if (option.value !== selectedValue) {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.textContent;
            newDropdown.appendChild(optionElement);
        }
    });

    // Enable the newly added dropdown
    newDropdown.disabled = false;
}

function populateSecondDropdown(dropdownIndex = null) {
    console.log('populateSecondDropdown() called');

    const categoryDropdown = document.getElementById('category');
    const category = categoryDropdown ? categoryDropdown.value : null;

    if (!category) {
        console.error('Category dropdown not found or has no value.');
        return;
    }

    fetch(`fetch_fund_names?category=${category}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {

        console.log("data:", data);

        // Update the fund_name dropdown if it's not disabled
        const fundNameDropdown = document.getElementById('fund_name');
        console.log("fundNameDropdown:", fundNameDropdown);

        if (fundNameDropdown) {
            console.log("fundNameDropdown 1:", fundNameDropdown);
            updateDropdownOptions(fundNameDropdown, data);
        }

        // Update additional dropdowns if dropdownIndex is not null
        if (dropdownIndex !== null) {
            const additionalDropdown = document.getElementById(`dropdown_${dropdownIndex}`);
            if (additionalDropdown) {
                updateDropdownOptions(additionalDropdown, data);
            }
        } else {
            // Update all additional dropdowns
            for (let i = 3; i <= 5; i++) {
                const dropdown = document.getElementById(`dropdown_${i}`);
                if (dropdown) {
                    updateDropdownOptions(dropdown, data);
                }
            }
        }

        // Enable all dropdowns
        enableDropdowns();

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function updateDropdownOptions(dropdown, options) {
    dropdown.innerHTML = ''; // Clear existing options

    console.log("In the updateDropdownOptions!!!!!!!!!!!!!!!!");

    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        dropdown.appendChild(optionElement);
    });
}

function enableDropdowns() {
    const dropdowns = document.querySelectorAll('select:not(#category)');
    dropdowns.forEach(dropdown => {
        dropdown.disabled = false;
    });

    // Enable the add dropdown button
    const addButton = document.getElementById('btn-add-dropdown');
    if (addButton) {
        addButton.disabled = false;
    }
}

function compare() {
    // Collect values from category and fund_name dropdowns
    const category = document.getElementById('category').value;
    const fundName = document.getElementById('fund_name').value;

    // Collect values from additional dropdowns, if present
    const additionalDropdownValues = [];
    for (let i = 3; i <= 5; i++) {
        const dropdown = document.getElementById(`dropdown_${i}`);
        if (dropdown) {
            const dropdownValue = dropdown.value;
            if (dropdownValue) {
                additionalDropdownValues.push(dropdownValue);
            }
        }
    }

    console.log('category-', category)
    console.log('fundName-', fundName)
    console.log('additionalDropdownValues-', additionalDropdownValues)

    // Combine all fund names including the fund_name dropdown and additional dropdowns
    const allFundNames = [fundName, ...additionalDropdownValues].filter(value => value !== '');
    console.log('allFundNames-', allFundNames)

    // Make AJAX request to Flask server for comparison
    fetch(`/compare?category=${category}&fund_name=${allFundNames}`)
        .then(response => {
            console.log("response:", response)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Process the fetched data and display comparison results
            console.log('Comparison results:', data);
            const numColumns = data.length > 0 ? data[0].length : 0; // Determine the number of columns
            displayComparisonResults(data, numColumns); // Pass numColumns to the displayComparisonResults function
        })
        .catch(error => {
            console.error('Error comparing funds:', error);
        });
}

function displayComparisonResults(data, numColumns) {
    const tableBody = document.querySelector('#comparison-table tbody');
    tableBody.innerHTML = ''; // Clear existing table body

    // Create table headers dynamically
    const tableHeader = document.querySelector('#comparison-table thead');
    tableHeader.innerHTML = ''; // Clear existing table header
    const headerRow = document.createElement('tr');

    // Define column names based on the number of columns
    let columnNames;
    if (numColumns === 4) {
        columnNames = ['ISIN No', 'Stock Name', 'Stock Count', 'Fund Names List'];
    } else if (numColumns === 3) {
        columnNames = ['ISIN No', 'Stock Name', 'Fund Names'];
    } else {
        columnNames = Array.from({ length: numColumns }, (_, i) => `Column ${i + 1}`);
    }

    // Populate table headers with column names
    columnNames.forEach(columnName => {
        const headerCell = document.createElement('th');
        headerCell.textContent = columnName;
        headerRow.appendChild(headerCell);
    });
    tableHeader.appendChild(headerRow);

    // Populate table with comparison results
    data.forEach(rowData => {
        const newRow = document.createElement('tr');
        rowData.forEach(value => {
            const newCell = document.createElement('td');
            newCell.textContent = value;
            newRow.appendChild(newCell);
        });
        tableBody.appendChild(newRow);
    });
}

function removeDropdown() {

    console.log("CLicked!!!!!!!!!!!!!!!!!!!!!!!!!!")

    const dropdownContainer = document.querySelector('.search-form');
    const dropdowns = dropdownContainer.querySelectorAll('.dropdown');
    const dropdownCount = dropdowns.length;

    if (dropdownCount > 2) { // Ensure there are more than two dropdowns (category and fund name)
        const lastDropdown = dropdowns[dropdownCount - 1];
        dropdownContainer.removeChild(lastDropdown);
    }

    // Disable the "Remove Dropdown" button if there are only two dropdowns left
    const removeButton = document.getElementById('btn-remove-dropdown');
    removeButton.disabled = dropdownContainer.querySelectorAll('.dropdown').length <= 2;

    // Enable the "Add Dropdown" button when a dropdown is removed
    const addButton = document.getElementById('btn-add-dropdown');
    addButton.disabled = false;
}


// Add event listener to the Compare button
document.getElementById('btn-compare').addEventListener('click', compare);
