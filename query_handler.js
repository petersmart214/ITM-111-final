

const iframe_elem = document.getElementById("query_iframe");
let message = "Hit a button to run a query! Some may take a significant amount of time!";


function change_query(new_query, new_message) {
    message = new_message
    document.getElementById("message_box").innerHTML = "<h3>Loading....</h3>";
    iframe_elem.src = `${iframe_elem.getAttribute("data-src")}/${new_query}`;
}


iframe_elem.addEventListener("load", () => {
  document.getElementById("message_box").innerHTML = message;
  console.log(iframe_elem.contentDocument)
  document.getElementById("error_box").textContent = iframe_elem.document.getElementById("error_container").textContent
});

