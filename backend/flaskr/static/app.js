/* const checkboxes = document.querySelectorAll(".check-completed");
for (let i = 0; i < checkboxes.length; i++) {
  const checkbox = checkboxes[i];
  checkbox.onchange = function (e) {
    console.log("event", e);
    const newCompleted = e.target.checked;
    const todoId = e.target.dataset["id"];
    fetch("/todo/" + todoId + "/set-completed", {
      method: "POST",
      body: JSON.stringify({
        completed: newCompleted,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(function () {
        document.getElementById("errors-todos").className = "hidden";
        window.location.reload(true);
      })
      .catch(function (err) {
        console.log(err);
        document.getElementById("errors-todos").className = "";
      });
  };
} */
/* const checkboxesList = document.querySelectorAll(".list-completed");
for (let i = 0; i < checkboxesList.length; i++) {
  const checkbox = checkboxesList[i];
  checkbox.onchange = function (e) {
    console.log("event", e);
    const newCompleted = e.target.checked;
    const listId = e.target.dataset["id"];
    fetch("/lists/" + listId + "/set-completed", {
      method: "POST",
      body: JSON.stringify({
        completed: newCompleted,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(function () {
        document.getElementById("errors-lists").className = "hidden";
        window.location.reload(true);
      })
      .catch(function (err) {
        console.log(err);
        document.getElementById("errors-lists").className = "";
      });
  };
} */
/* const descInput = document.getElementById("description-todo");
const activeList = document.getElementById("active-list");
document.getElementById("form-todo").onsubmit = function (e) {
  e.preventDefault();
  const desc = descInput.value;
  const actList = activeList.dataset["id"];
  descInput.value = "";
  fetch("/todo/create", {
    method: "POST",
    body: JSON.stringify({
      description: desc,
      active_list: actList,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (jsonResponse) {
      console.log("response", jsonResponse);
      li = document.createElement("li");
      li.innerText = desc;
      document.getElementById("todos").appendChild(li);
      document.getElementById("errors-todos").className = "hidden";
      window.location.reload(true);
    })
    .catch(function (err) {
      console.log(err);
      document.getElementById("errors-todos").className = "";
    });
}; */
const descInputMovie = document.getElementById("description-movie");
const relDateInput = document.getElementById("release-date");
document.getElementById("form-movie").onsubmit = function (e) {
  e.preventDefault();
  const title = descInputMovie.value;
  const relDate = relDateInput.value;
  descInputMovie.value = "";
  fetch("/movies/create", {
    method: "POST",
    body: JSON.stringify({
      title: title,
      release_date: relDate
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (jsonResponse) {
      console.log("response", jsonResponse);
      li = document.createElement("li");
      li.innerText = name;
      document.getElementById("movies").appendChild(li);
      document.getElementById("errors-movie").className = "hidden";
      window.location.reload(true);
    })
    .catch(function (err) {
      console.log(err);
      document.getElementById("errors-movie").className = "";
    });
};
/* document.addEventListener("click", function(evnt){
                      console.log(evnt.target.id);
                      id = evnt.target.id;
                      fetch('/todo/'+ id, {
                              method: 'DELETE'
                          })
                          .then(function() {
                              document.getElementById('errors').className = 'hidden';
                          })
                          .catch(function(err) {
                              console.log(err)
                              document.getElementById('errors').className = '';
                          })
                  }); */
const deleteBtns = document.querySelectorAll(".delete-button-movie");
for (let i = 0; i < deleteBtns.length; i++) {
  const btn = deleteBtns[i];
  btn.onclick = function (e) {
    const movieId = e.target.dataset["id"];
    fetch("/movies/" + movieId, {
      method: "DELETE",
    }).then(function (response) {
      e.target.parentNode.remove();
    });
  };
}
const deleteBtnsAct = document.querySelectorAll(".delete-button-actor");
for (let i = 0; i < deleteBtnsAct.length; i++) {
  const btn = deleteBtnsAct[i];
  btn.onclick = function (e) {
    const actorId = e.target.dataset["id"];
    fetch("/actors/" + actorId, {
      method: "DELETE",
    }).then(function (response) {
      e.target.parentNode.remove();
    });
  };
}