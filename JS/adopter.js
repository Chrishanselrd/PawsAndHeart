function searchDatabase() {
    // Get form input values
    const animalType = document.getElementById("animalType").value;
    const animalAge = document.getElementById("age").value;

    // Make an AJAX request to the server
    const xhr = new XMLHttpRequest();

    // Define the server-side script URL (replace with your actual server-side script URL)
    const url = "searchDatabase.php"; // Replace with your server-side script URL

    // Create the data to send to the server
    const data = `animalType=${encodeURIComponent(
      animalType
    )}&animalAge=${encodeURIComponent(animalAge)}`;

    // Set up the AJAX request
    xhr.open("POST", url, true);
    xhr.setRequestHeader(
      "Content-Type",
      "application/x-www-form-urlencoded"
    );

    // Set up the callback function for when the request is complete
    xhr.onload = function () {
      if (xhr.status === 200) {
        // Update the searchResults div with the response from the server
        document.getElementById("searchResults").innerHTML =
          xhr.responseText;
      } else {
        // Handle errors
        console.error("Error making AJAX request:", xhr.statusText);
      }
    };

    // Send the request to the server
    xhr.send(data);
  }