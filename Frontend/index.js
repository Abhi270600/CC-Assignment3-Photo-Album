var name = '';
var encoded = null;
var fileExt = null;

// Testing Codepipeline 2


function search() {
  var searchTerm = document.getElementById("searchbar").value;
  var apigClient = apigClientFactory.newClient({ apiKey: "dsi26xlHu41UqcoVGkCmz57U6xA39egI719YrY4c" });


    var body = { };
    var params = {q : searchTerm};
    var additionalParams = {
      headers: {
        'Content-Type': 'application/json'
      }
    };

    apigClient.searchGet(params, body , additionalParams).then(function(res){
        console.log("success");
        console.log(res);
        showImages(res.data)
      }).catch(function(result){
          console.log(result);
          console.log("NO RESULT");
      });

}

/////// SHOW IMAGES BY SEARCH //////

function showImages(res) {
  var newDiv = document.getElementById("images");
  if (newDiv) {
      newDiv.innerHTML = ''; // Clear previous results
  }

  console.log(res);

  // Parse the JSON string in res.body
  let data;
  try {
      data = JSON.parse(res.body);
  } catch (e) {
      console.error("Error parsing JSON:", e);
      data = [];
  }

  if (data.length === 0) {
      var noResults = document.createElement("p");
      noResults.textContent = "No images found";
      noResults.style.textAlign = "center";
      noResults.style.width = "100%";
      newDiv.appendChild(noResults);
  } else {
      // Create a container for the images
      var imagesContainer = document.createElement("div");
      imagesContainer.style.display = "flex";
      imagesContainer.style.flexWrap = "wrap";
      imagesContainer.style.justifyContent = "center";
      imagesContainer.style.gap = "20px";
      imagesContainer.style.width = "100%";

      // Iterate over the parsed array
      for (var i = 0; i < data.length; i++) {
          var imageKey = data[i].objectKey;

          if (!imageKey) {
              console.warn(`Missing object key for item at index ${i}`, data[i]);
              continue;
          }

          var newimg = document.createElement("img");
          
          // Remove random size classes or use consistent ones
          newimg.style.width = "250px";
          newimg.style.height = "250px";
          newimg.style.objectFit = "cover";
          
          // Extract the filename
          var filename = imageKey.substring(imageKey.lastIndexOf('/') + 1);
          
          // Set the image source
          newimg.src = "https://my-b2-photos.s3.us-east-1.amazonaws.com/" + filename;
          newimg.alt = "Search result image";
          newimg.loading = "lazy"; // Add lazy loading
          
          // Append the image to the container
          imagesContainer.appendChild(newimg);
      }
      
      // Append the container to the main div
      newDiv.appendChild(imagesContainer);
  }
}


function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}



function toggleCustomLabelInput() {
  var customLabelsInput = document.getElementById('customLabels');
  if (customLabelsInput.style.display === 'none' || customLabelsInput.style.display === '') {
    customLabelsInput.style.display = 'block';
  } else {
    customLabelsInput.style.display = 'none';
  }
}

///// UPLOAD IMAGES ///////

const realFileBtn = document.getElementById("realfile");
function uploadImage() {
  // No need to display the custom labels input since it's already visible
  realFileBtn.click(); 
}

function previewFile(input) {
  var file = input.files[0];
  var reader = new FileReader();
  var name = file.name;
  var fileExt = name.split(".").pop().toLowerCase();
  var onlyname = name.replace(/\.[^/.]+$/, "");
  var finalName = onlyname + "." + fileExt;

  console.log("File extension:", fileExt);
  console.log("Final filename:", finalName);

  // Check if the file is an image
  if (!['jpg', 'jpeg', 'png'].includes(fileExt)) {
    alert("Please select a valid image file (JPG, JPEG, or PNG).");
    return;
  }

  var customLabels = document.getElementById('customLabels').value;
  console.log("Custom Labels:", customLabels);

  reader.onload = function(e) {
    var apigClient = apigClientFactory.newClient({
      apiKey: "dsi26xlHu41UqcoVGkCmz57U6xA39egI719YrY4c"
    });

    var params = {
      "bucket": "my-b2-photos",
      "filename": finalName
    };

    var additionalParams = {
      headers: {
        "Content-Type": file.type,
        "x-amz-meta-customLabels": customLabels,
      }
    };
    body = btoa(e.target.result);
    apigClient.uploadBucketFilenamePut(params, body, additionalParams)
      .then(function(result) {
        console.log('Reader body : ', body);
        console.log("Upload result:", result);
        alert("Photo Uploaded Successfully");
        // Clear the custom labels input
        document.getElementById('customLabels').value = '';
      })
      .catch(function(error) {
        console.error("Upload error:", error);
        alert("Photo Upload Failed: " + error.message);
      });
  };
  reader.readAsBinaryString(file);
}