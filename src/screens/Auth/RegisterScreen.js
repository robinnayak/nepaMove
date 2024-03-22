import React, { useEffect ,useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
// import axios from "axios";
import { CheckBox } from "react-native-elements";
import axios from "axios";
import { BASEURL, Register,CSRFTOKEN } from "../../services/Baseurl";

const RegisterScreen = ({ navigation }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password1, setPassword1] = useState("");
  const [is_driver, setIsDriver] = useState(false);
  const [user, setUser] = useState("");
  const [csrftoken, setCsrfToken] = useState("");

  useEffect(() => {
    const getToken = async () => {
      const res = await axios.get(BASEURL + CSRFTOKEN);
      const token = res.data.csrfToken;
      console.log(token);
      setCsrfToken(token);
    };
    getToken();
  }, []);
  const handleRegister = async ({navigation}) => {
    try {
      const userData = {
        username,
        email,
        password,
        password1,
        phone_number: "",
        is_driver: is_driver,
      };
      const token = csrftoken;
      const response = await axios.post(BASEURL + Register, userData, {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": token,
        },
      });
      // const res = await axios.get('http://10.0.2.2:8000/register/')
      setUser(response.data);
      console.log("Registration successful: ", response.data);

      console.log("user data", user);
      navigation.navigate('Login')
    } catch (err) {
      console.error("Registeration Error: ", err);
    }
  };
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Username</Text>

      <TextInput
        style={styles.input}
        value={username}
        onChangeText={setUsername}
        placeholder="Enter your username"
      />

      <Text style={styles.label}>Email</Text>
      <TextInput
        style={styles.input}
        value={email}
        onChangeText={setEmail}
        placeholder="Enter your email"
        keyboardType="email-address"
      />

      <Text style={styles.label}>Password</Text>
      <TextInput
        style={styles.input}
        value={password}
        onChangeText={setPassword}
        placeholder="Enter your password"
        secureTextEntry
      />

      <Text style={styles.label}>Confirm Password</Text>
      <TextInput
        style={styles.input}
        value={password1}
        onChangeText={setPassword1}
        placeholder="Confirm your password"
        secureTextEntry
      />
      <CheckBox
        title="Are you a driver?"
        checked={is_driver}
        onPress={() => setIsDriver(!is_driver)}
      />
      <Button title="Register" onPress={handleRegister} />

      <Text style={styles.link} onPress={() => navigation.navigate("Login")}>
        Already have an account? Login here
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 16,
  },
  label: {
    fontSize: 16,
    marginVertical: 8,
  },
  input: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    marginBottom: 16,
    paddingHorizontal: 8,
  },
  link: {
    marginTop: 16,
    color: "blue",
    textDecorationLine: "underline",
  },
});

export default RegisterScreen;
