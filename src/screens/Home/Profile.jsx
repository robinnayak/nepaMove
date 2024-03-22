import React, { useEffect, useState } from "react";
import { Text, View, StyleSheet, Button } from "react-native";
import axios from "axios";
import { BASEURL, Driver, LOGOUT } from "../../services/Baseurl";

const Profile = ({ route,navigation }) => {
  const [userData, setUserData] = useState(null);
  const [csrftoken,setCsrfToken] = useState(route.params.token);


  useEffect(() => {
    const getDriverUserData = async () => {
      try {
        const response = await axios.get(BASEURL + Driver + route.params.username);
        setUserData(response.data.user);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };
    getDriverUserData();
  }, [route.params.username]);
  const handleLogout = async ()=>{
    const res = await axios.get(BASEURL+LOGOUT)
    if (res.data.is_logout){
      console.log("logout data",res.data)
      navigation.navigate('Login')
    }
  }
  return (
    <View style={styles.container}>
      {userData ? (
        <View>
          <Text style={styles.header}>Profile view</Text>
          {userData.user.is_driver ? (
            <View style={styles.driverProfile}>
              <Text style={styles.greeting}>
                Hello, <Text style={styles.username}>{userData.user.username}</Text>
              </Text>
              <Text style={styles.dataItem}>Email: {userData.user.email}</Text>
              <Text style={styles.dataItem}>Phone Number: {userData.phone_number}</Text>
              <Text style={styles.dataItem}>License Number: {userData.license_number}</Text>
              <Text style={styles.dataItem}>Address: {userData.address}</Text>
              <Text style={styles.dataItem}>Date of Birth: {userData.date_of_birth}</Text>
              <Text style={styles.dataItem}>Driving Experience: {userData.driving_experience} years</Text>
              <Button title="logout" onPress={handleLogout} />
              <View></View>
              <Button title="Edit" onPress={()=>navigation.navigate('Edit',{user:userData,token:csrftoken})} />
              {/* Add more data items as needed */}
            </View>
          ) : (
            <Text style={styles.passengerProfile}>Passenger profile</Text>
          )}
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
      
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
    alignItems: "center",
  },
  header: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },
  greeting: {
    fontSize: 16,
    marginBottom: 20,
  },
  username: {
    color: "purple",
  },
  driverProfile: {
    // Styles for the driver profile
  },
  passengerProfile: {
    // Styles for the passenger profile
  },
  dataItem: {
    fontSize: 14,
    marginBottom: 10,
  },
});

export default Profile;
