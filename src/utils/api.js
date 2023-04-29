import { toast } from "react-toastify";

export const baseurl = "https://vincinemaApi.pythonanywhere.com/";

export const login = (email, password) => {
  fetch(`${baseurl}login?username=${email}&password=${password}`, {
    method: "POST",
  })
    .then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          console.log(data);
          localStorage.setItem("token", data["token"]);
          localStorage.setItem("validDue", data["validDue"]);
          localStorage.setItem("email", email);
          //document.location.href = '/profile';;
        });
      } else {
        toast.error("Wrong username or password");
      }
    })
    .catch((err) => console.error(err));
};
