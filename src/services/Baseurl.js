import axios from "axios";

//base url
export const BASEURL = "http://10.0.2.2:8000/";
//auth
export const Register = "register/";
export const Login = "login/";
export const LOGOUT = "logout/";
export const CSRFTOKEN = "get-csrf-token/";
//Driver part
export const PROFILE = "";
export const Driver = "driver/";

// auth csrf token
export const csrf_token = async () => {
  try {
    const res = await axios.get(BASEURL + CSRFTOKEN);
    const token = res.data.csrfToken;
    // console.log("res data",res.data.csrfToken)

    return token;
  } catch (err) {
    console.error("Error Fetchin CSRF token", err);
    throw err;
  }
};
