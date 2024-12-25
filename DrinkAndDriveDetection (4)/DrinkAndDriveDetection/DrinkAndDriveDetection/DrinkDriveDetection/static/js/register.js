document.addEventListener('DOMContentLoaded', function () {
    const countrySelect = document.getElementById('id_country');
    const stateSelect = document.getElementById('id_state');
    const citySelect = document.getElementById('id_city');

    const fetchData = async (url, targetSelect, defaultOption, disable = false) => {
        targetSelect.innerHTML = `<option>Loading...</option>`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            targetSelect.innerHTML = `<option value="">${defaultOption}</option>`;
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id;
                option.text = item.name;
                targetSelect.appendChild(option);
            });
            targetSelect.disabled = disable ? data.length === 0 : false;
        } catch (error) {
            console.error(`Error fetching ${defaultOption.toLowerCase()}:`, error);
            targetSelect.innerHTML = `<option value="">Error loading ${defaultOption.toLowerCase()}</option>`;
        }
    };

    countrySelect.addEventListener('change', function () {
        const countryId = this.value;
        stateSelect.innerHTML = `<option value="">Select State</option>`;
        citySelect.innerHTML = `<option value="">Select City</option>`;
        citySelect.disabled = true;
        if (countryId) {
            fetchData(`/get_states/${countryId}/`, stateSelect, 'Select State');
        }
    });

    stateSelect.addEventListener('change', function () {
        const stateId = this.value;
        citySelect.innerHTML = `<option value="">Select City</option>`;
        if (stateId) {
            fetchData(`/get_cities/${stateId}/`, citySelect, 'Select City');
        }
    });
});
