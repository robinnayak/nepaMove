import axios from "axios";
import { useEffect, useState } from "react";
import {
  TextInput,
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { CheckBox } from "react-native-elements";
import { BASEURL, CSRFTOKEN, Driver } from "../../services/Baseurl";

const Edit = ({ route, navigation }) => {
  const [userData, setUserData] = useState(route.params.user);
  const [username, setUsername] = useState(userData.user.username);
  const [email, setEmail] = useState(userData.user.email);
  const [phone_number, setPhoneNumber] = useState(userData.phone_number);
  const [license_number, setLicenseNumber] = useState(userData.license_number);
  const [address, setAddress] = useState(userData.address);
  const [dob, setDob] = useState(userData.date_of_birth);
  const [driving_experience, setDrivingExperience] = useState(
    userData.driving_experience.toString()
  );
  const [earnings, setEarnings] = useState(userData.earnings.toString());
  const [rating, setRating] = useState(userData.rating.toString());
  const [total_rides, setTotalRides] = useState(
    userData.total_rides.toString()
  );
  const [availability_status, setAvailabilityStatus] = useState(
    userData.availability_status
  );
  const [last_updated_location, setUpdatedLocation] = useState(
    userData.last_updated_location
  );
  const [csrftoken, setCsrfToken] = useState(route.params.token);
  // const [csrftoken, setCsrfToken] = useState(null);

  console.log("edit page data", userData);
  const handleSubmit = async () => {
    try {
      const updatedData = {
        address,
        availability_status,
        date_of_birth: dob,
        driving_experience: parseInt(driving_experience),
        earnings: parseFloat(earnings),
        last_updated_location,
        license_number,
        phone_number,
        rating: parseFloat(rating),
        total_rides: parseInt(total_rides),
      };
      // const response = await axios.put(BASEURL + Driver + route.params.username);
      const res = await axios.put(
        BASEURL + Driver + username + "/",
        updatedData,
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
        }
        );
        //need to put token
        console.log("updated date", res.data);
        navigation.navigate("Profile");
      } catch (error) {
      if (error.response) {
        console.error("Backend Error: ");
        console.error("Response Data: ", error.response.data);
        console.error("Response status: ", error.response.status);
        console.error("Response headers: ", error.response.headers);
        if (
          error.response.status === 403 &&
          error.response.data.detail ===
            "CSRF Failed: CSRF token missing or incorrect."
        ) {
          console.error(
            "CSRF token error: The CSRF token is missing or incorrect"
          );
        } else if (error.response.status === 401) {
          console.error("Authentication error: User not authenticated");
        } else {
          console.error(
            "Authorization error: User lacks necessary permissions"
          );
        }
      } else if (error.request) {
        console.error("Backend error: No response received");
      } else {
        console.error("Frontend Error: ");
        console.error("Error message: ", error.message);
      }
      console.error("Error config: ", error.config);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>
          {" "}
          Edit Profile: {username} - {csrftoken}
        </Text>
        <Text style={styles.label}>Address :</Text>
        <TextInput
          value={address}
          onChangeText={(text) => setAddress(text)}
          style={styles.input}
        />
        <Text>Phone Number: </Text>
        <TextInput
          value={phone_number}
          onChangeText={(text) => setPhoneNumber(text)}
          style={styles.input}
        />
        <Text>License Number: </Text>
        <TextInput
          value={license_number}
          onChangeText={(text) => setLicenseNumber(text)}
          style={styles.input}
        />
        <Text>Date of Birth: </Text>
        <TextInput
          value={dob}
          onChangeText={(text) => setDob(text)}
          style={styles.input}
        />
        <Text>Driving Expereince: </Text>
        <TextInput
          value={driving_experience}
          onChangeText={(text) => setDrivingExperience(text)}
          style={styles.input}
        />
        <Text>Total Rides: </Text>
        <TextInput
          value={total_rides}
          onChangeText={(text) => setTotalRides(text)}
          style={styles.input}
        />
        <Text>Earnings: </Text>
        <TextInput
          value={earnings}
          onChangeText={(text) => setEarnings(text)}
          style={styles.input}
        />
        <Text>Rating: </Text>
        <TextInput
          value={rating}
          onChangeText={(text) => setRating(text)}
          style={styles.input}
        />
        <Text>Last updated: </Text>
        <TextInput
          value={last_updated_location}
          onChangeText={(text) => setUpdatedLocation(text)}
          style={styles.input}
          disable
        />
      </View>
      <CheckBox
        title="Are you a driver?"
        checked={availability_status}
        onPress={() => setAvailabilityStatus(!availability_status)}
      />
      <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
        <Text style={styles.submitButtonText}>Submit</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#f4f4f4", // Background color
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 10,
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
    color: "#333",
  },
  input: {
    height: 40,
    borderColor: "#ccc",
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    borderRadius: 5,
    backgroundColor: "#fff", // Input background color
  },
  submitButton: {
    backgroundColor: "#007bff", // Submit button background color
    paddingVertical: 15,
    borderRadius: 8,
  },
  submitButtonText: {
    color: "#fff", // Submit button text color
    textAlign: "center",
    fontSize: 18,
    fontWeight: "bold",
  },
});

export default Edit;
