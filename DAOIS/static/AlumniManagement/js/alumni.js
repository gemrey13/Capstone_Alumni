
  const modal = document.querySelector('.modal');
  const showModal = document.querySelector('.showModal');
  const closeModal = document.querySelectorAll('.closeModal');

  showModal.addEventListener('click', function (){
    modal.classList.remove('hidden')
  });

  closeModal.forEach(close => {
    close.addEventListener('click', function (){
      modal.classList.add('hidden')
    });
  })


  $(document).ready(function() {
    $('#search-form').submit(function(event) {
        event.preventDefault();
        var query = $('#search-input').val();
        console.log(query)
        $.ajax({
            type: 'GET',
            url: '/alumni/search/',
            data: {
                'query': query
            },
            success: function(response) {
                $('#table-container').html(response.html),
                $('#card-container').html(response.html);
            },
            error: function(xhr, status, error) {
                // Handle error if needed
            }
        });
    });
});


    $(document).ready(function() {
      // Triggered when the country selection changes
      $('#country').change(function() {
        var countryId = $(this).val();
        if (countryId !== '') {
          // Fetch provinces for the selected country
          $.ajax({
            url: '/get_provinces/',
            type: 'GET',
            data: { country_id: countryId },
            success: function(response) {
              // Clear previous options
              $('#province').empty().append('<option value="">Select Province</option>');
              $('#city').empty().append('<option value="">Select City</option>');
              $('#barangay').empty().append('<option value="">Select Barangay</option>');

              // Populate provinces
              response.provinces.forEach(function(province) {
                $('#province').append('<option value="' + province.id + '">' + province.province_name + '</option>');
              });
            }
          });
        } else {
          // Clear province, city, and barangay options if country is not selected
          $('#province').empty().append('<option value="">Select Province</option>');
          $('#city').empty().append('<option value="">Select City</option>');
          $('#barangay').empty().append('<option value="">Select Barangay</option>');
        }
      });

      // Triggered when the province selection changes
      $('#province').change(function() {
        var provinceId = $(this).val();
        if (provinceId !== '') {
          // Fetch cities for the selected province
          $.ajax({
            url: '/get_cities/',
            type: 'GET',
            data: { province_id: provinceId },
            success: function(response) {
              // Clear previous options
              $('#city').empty().append('<option value="">Select City</option>');
              $('#barangay').empty().append('<option value="">Select Barangay</option>');

              // Populate cities
              response.cities.forEach(function(city) {
                $('#city').append('<option value="' + city.id + '">' + city.city_name + '</option>');
              });
            }
          });
        } else {
          // Clear city and barangay options if province is not selected
          $('#city').empty().append('<option value="">Select City</option>');
          $('#barangay').empty().append('<option value="">Select Barangay</option>');
        }
      });

      // Triggered when the city selection changes
      $('#city').change(function() {
        var cityId = $(this).val();
        if (cityId !== '') {
          // Fetch barangays for the selected city
          $.ajax({
            url: '/get_barangays/',
            type: 'GET',
            data: { city_id: cityId },
            success: function(response) {
              // Clear previous options
              $('#barangay').empty().append('<option value="">Select Barangay</option>');

              // Populate barangays
              response.barangays.forEach(function(barangay) {
                $('#barangay').append('<option value="' + barangay.id + '">' + barangay.barangay_name + '</option>');
              });
            }
          });
        } else {
          // Clear barangay options if city is not selected
          $('#barangay').empty().append('<option value="">Select Barangay</option>');
        }
      });
    });
