document.addEventListener("DOMContentLoaded", function() {
    // Selecting the element with the class ".col-sm-1.col-xs-1.heading-dot.pull-right"
    const optiontick = document.querySelector(".col-sm-1.col-xs-1.heading-dot.pull-right");

    // Adding a click event listener to the selected element
    optiontick.addEventListener("click", function() {
        console.log("Element clicked");
        // Selecting the element with the class ".optionbox"
        const optionbox = document.querySelector(".optionbox");

        if (optionbox.style.visibility === "hidden") {
optionbox.style.visibility = "visible";

}

        else optionbox.style.visibility = "hidden";
        
     
    });
    const logout=document.querySelector("#logout");
     logout.addEventListener("click",function(){
          console.log(logout.value);
          window.location.href = redirectUrl;
     });

     var linkElement = document.querySelector(".previous");
     if (linkElement) {
       linkElement.addEventListener("click", function() {
        console.log("clicked");
         var scrollableDiv = document.getElementById("conversation");
         scrollableDiv.scrollTop = 0;
       });
     }
});
$(function () {
    $(".heading-compose").click(function () {
      $(".side-two").css({
        left: "0",
      });
    });

    $(".newMessage-back").click(function () {
      $(".side-two").css({
        left: "-100%",
      });
    });
  });
  
 
 // Assuming this JavaScript file is loaded after the HTML
document.addEventListener("DOMContentLoaded", function() {
    
  });
  
 