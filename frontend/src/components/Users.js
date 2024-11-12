import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Users() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        // Realiza la solicitud al endpoint que creaste en el backend
        axios.get('http://localhost:8000//api/usersProfile/non-staff-users/') 
            .then(response => {
                setUsers(response.data);
            })
            .catch(error => {
                console.error('Error fetching non-staff users:', error);
            });
    }, []);

    return (
        <div>
            <h1>Users</h1>
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.user.username}</li>
                ))}
            </ul>
        </div>
    );
}

export default Users;
