import {useEffect} from "react";
import axios from "axios";

export const Logout = () => {
    useEffect(() => {
       (async () => {
         try {
           await axios.post(
             'http://localhost:8000/api/logout/',
             { refresh_token: localStorage.getItem('refresh_token') },
             {
               headers: {'Content-Type': 'application/json'},
               withCredentials: true
             }
           );
           
           // Clear the tokens and unset authentication
           localStorage.clear();
           axios.defaults.headers.common['Authorization'] = null;

           // Redirect to login
           window.location.href = '/login';
         } catch (e) {
           console.log('Logout not working', e);
         }
       })();
    }, []);

    return <div></div>;
};
