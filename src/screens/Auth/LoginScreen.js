import React, { useEffect, useState } from "react";
import { Text, View, Button, StyleSheet, TextInput } from "react-native";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import { BASEURL, Login, CSRFTOKEN } from "../../services/Baseurl";

const LoginScreen = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  // const [user, setUser] = useState();
  const [csrftoken, setCsrfToken] = useState("");
  
  const navigation = useNavigation();
  // const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  useEffect(() => {
    const getToken = async () => {
      const res = await axios.get(BASEURL + CSRFTOKEN);
      const token = res.data.csrfToken;
      console.log(token);
      setCsrfToken(token);
    };
    getToken();
  }, []);
  const handleLogin = async () => {
    try {
      const users = {
        username,
        password,
      };
      const token = csrftoken;
      console.log("token", token);
      const response = await axios.post(BASEURL + Login, users, {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": token,
        },
      });

      console.log(response.data);
      // setUser(response.data);
      // console.log("Login successful: ", user);
      navigation.navigate("Home",{user:response.data,token:csrftoken});
      
    } catch (err) {
      console.error("Login Error: ", err);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login Page!!</Text>

      <View>
        <Text style={styles.label}>Username</Text>
        <TextInput
          style={styles.input}
          value={username}
          onChangeText={setUsername}
          placeholder="Enter your username"
        />

        <Text style={styles.label}>Password</Text>
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          placeholder="Enter your password"
          secureTextEntry
        />

        <Button title="Login" onPress={handleLogin} />
      </View>

      <Text style={styles.link} onPress={() => navigation.navigate("Register")}>
        Don't have an account? Register here
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
    backgroundColor: "#F5FCFF", // Light background color
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 30,
    textAlign: "center", // Center the title
  },
  input: {
    backgroundColor: "#fff",
    borderColor: "#ccc",
    borderWidth: 1,
    borderRadius: 5,
    padding: 10,
    marginBottom: 15,
    maxWidth: "100%", // Ensure full width
  },
  label: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 5,
  },
  button: {
    backgroundColor: "#4CAF50", // Green button color
    color: "#fff",
    padding: 15,
    borderRadius: 5,
    marginTop: 20,
  },
  link: {
    fontSize: 14,
    color: "#333",
    textAlign: "center", // Center the link
  },
});

export default LoginScreen;
