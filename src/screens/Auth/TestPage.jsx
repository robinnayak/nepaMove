import axios from "axios"
import { useEffect, useState } from "react"
import { Text, View } from "react-native"

const TestPage = ()=>{
  const [user,Setuser] = useState('')

  useEffect(()=>{
    async function getUser(){
      try{
        const user = await axios.get('http://10.0.2.2:8000/register/')
        console.log(user.data)
        Setuser(user.data)
      }catch(err){
        console.error(err)
      }
    }
    getUser()
  },[])

  return(
    <View>
      <Text>Hello world</Text>
    </View>
  )
}
export default TestPage