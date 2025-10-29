let username_input = document.getElementById("id_username");
let password1_input = document.getElementById("id_password1");
let password2_input = document.getElementById("id_password2");

input_list = [username_input, password1_input, password2_input];
if (username_input) {


    input_list.forEach(input => {
        input.addEventListener("focus", () => {

            let helptext_id = input.id + "_helptext";
            let helptext = document.getElementById(helptext_id);
            helptext.style.display = "block";
            helptext.style.transform = "translateX(0px)";

        });
        input.addEventListener("blur", () => {
            let helptext_id = input.id + "_helptext";
            let helptext = document.getElementById(helptext_id);
            helptext.style.transform = "translateX(20px)";
            setTimeout(() => {
                helptext.style.display = "none";
            }, 500);

        });

    });
}
let close_buttons = document.getElementsByName("close-outline");
close_buttons.forEach(button => {
    button.addEventListener("click", () => {
        //go to home page
        window.location.href = "/";
    });
});

//when page refreshes, reset particles


