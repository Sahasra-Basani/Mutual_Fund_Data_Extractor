function search() {
  const category = document.getElementById('category').value;
  const fundName = document.getElementById('fund_name').value;
  console.log('Search clicked. Category:', category, 'Fund Name:', fundName);
  // Perform search based on category and fund name
}

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

    //newDropdown.addEventListener('change', populateNewDropdown);

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

function search() {
    const category = document.getElementById('category').value;
    const fundName = document.getElementById('fund_name').value;

    // Collect values from additional dropdowns
    const additionalDropdownValues = [];
    for (let i = 3; i <= 5; i++) {
        const dropdownValue = document.getElementById(`dropdown_${i}`).value;
        if (dropdownValue) {
            additionalDropdownValues.push(dropdownValue);
        }
    }

    // Make AJAX request to Flask server
    fetch(`/search?category=${category}&fund_name=${fundName}&additional_values=${additionalDropdownValues.join(',')}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Process the fetched data
            console.log('Search results:', data);
        })
        .catch(error => {
            console.error('Error searching:', error);
        });
}
