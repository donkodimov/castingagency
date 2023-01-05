window.addEventListener('load', function() {
  // Get the current URL
  let url = window.location.href;

  // Extract the access token from the URL
  let params = new URLSearchParams(url.split('#')[1]);
  let accessToken = params.get('access_token');
  let endpoint = document.getElementById('endpoint')


  const apiButton = document.getElementById('call-api');      
  apiButton.addEventListener('click', async () => {
      let endpointFin = endpoint.value

      fetch(`${endpointFin}`, {
          method: 'GET',
          headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + accessToken
              },
      }).then(function(response) {
          if (response.status === 200) {
              return response.json()
              
          } else {
              console.log("error")
          }
      }).then(function(data) {
      // The request was successful, so render the data in the output element
         document.getElementById('output').innerHTML = JSON.stringify(data, null, 2);
      }).catch(function(error) {
          console.log(error)
      });
      
});
});