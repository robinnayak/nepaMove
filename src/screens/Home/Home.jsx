import { useEffect, useState } from "react";
import { Text, View,Button } from "react-native";

const Home = ({ route,navigation }) => {
  const [user, setUser] = useState("");
  const [username, setUsername] = useState("");
  const [csrftoken,setCsrfToken] = useState(route.params.token);
  useEffect(() => {
    setUser(route.params.user);
    // console.log("route user", route.params);
    // console.log("route user1", route.params.user.data); //working properly 
    // console.log("setUser : ", user);
    setUsername(route.params.user.data.username)
    console.log("username",username)
  }, []);
  return (
    <View>
      <Text>Home page!!</Text>
      <Text>Hello <Text style={{color:"purple"}} >{username}</Text> </Text>
      <Button title="Profile" onPress={() => navigation.navigate("Profile",{username:username,token:csrftoken})} />
    </View>
  );
};

export default Home;
