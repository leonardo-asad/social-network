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

  // Follow / Unfollow Users
  document.querySelector("#follow-button").addEventListener('click', event => {
    console.log("Button clicked!")

    follow_button = event.target

    user_id = parseInt(follow_button.dataset.user)

    console.log(user_id)

    fetch(`follow/${user_id}`)
    .then(response => response.json())
    .then(data => {
      console.log(data)

      if (data.action == "followed") {
        follow_button.setAttribute('aria-pressed', "true")
        follow_button.className = "btn btn-primary btn-sm active"
        follow_button.innerHTML = "Unfollow"
      }
      else {
        follow_button.setAttribute('aria-pressed', "false")
        follow_button.className = "btn btn-primary btn-sm"
        follow_button.innerHTML = "Follow"
      }

      document.querySelector("#following").innerHTML = data.following
      document.querySelector("#followers").innerHTML = data.followers
    })

  })





});