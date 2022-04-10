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

        button = document.getElementById(`likes-${post_id}`);
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

  // Edit view
  document.querySelectorAll("#edit-button").forEach(edit_button => {
    edit_button.addEventListener('click', () => {
      console.log("Button clicked!")
      post_id = edit_button.dataset.post
      console.log(post_id)

      // Make text edition area visible and hide post
      post_container = document.getElementById(post_id)
      edit_container = document.getElementById(`edit-${post_id}`)

      post_container.style.display = 'none'
      edit_container.style.display = 'block'

      submit_button = document.getElementById(`submit-${post_id}`)

      fetch(`edit/${parseInt(post_id)}`)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        post_form = document.getElementById(`edit-form-${post_id}`)
        post_form.innerHTML = data.post_content
      });
    });
  });

  // Submit edited post
  document.querySelectorAll("#submit-edited-post").forEach(submit_button => {
    submit_button.addEventListener('click', () => {
      console.log("Submit edited post!")

      post_id = submit_button.dataset.post
      console.log(post_id)

      post_form = document.getElementById(`edit-form-${post_id}`)
      updated_content = post_form.value

      fetch(`edit/${parseInt(post_id)}`, {
        method: "POST",
        body: JSON.stringify({
          content: updated_content
        })
      })
      .then(() => {
        post_container.style.display = 'block'
        edit_container.style.display = 'none'

        content = document.getElementById(`content-${post_id}`)
        content.innerHTML = updated_content
      });
    });
  });
});
