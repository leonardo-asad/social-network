document.addEventListener("DOMContentLoaded", function() {

  // Like / Unlike Posts
  document.querySelectorAll(".post-like-button").forEach(like_button => {
    like_button.addEventListener('click', () => {

      // Get the url to make the fetch
      href = like_button.dataset.href;
      console.log("Button clicked!");

      // Request to the url
      fetch(href)
      .then(response => response.json())
      .then(data => {
        post_id = data.post_id;
        console.log(`Post Id: ${post_id}`);
        console.log(data.action);

        button = document.getElementById(post_id);
        button.innerHTML = data.likes;

        // Change icon color according the state (liked, not liked)
        if (data.action === "unliked") {
          like_button.setAttribute("fill", "grey");
        }
        else {
          like_button.setAttribute("fill", "red");
        }
      });
    });
  });
});
