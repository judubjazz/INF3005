delete_post=(post_id)=>{
    let url = "http://localhost:5000/mypet";
    let username = document.getElementById('username').value;
    let name = document.getElementById('name').value;
    let family_name = document.getElementById('family_name').value;
    let phone = document.getElementById('phone').value;
    let adress = document.getElementById('adress').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
            username:username,
            name: name,
            family_name : family_name,
            phone : phone,
            adress : adress,
            email : email,
            password : password }),

    };

    return fetch(url, requestOptions)
        .then(response =>response.json())
        .catch(err=>{
            console.log("error :" + err)
        })
        .then(res=>{
            console.log(res);
            window.location = res.url;
        })
};