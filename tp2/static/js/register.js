register = () =>{
    let url = "http://localhost:5000/register";
    let username = document.getElementById('username').value;
    let name = document.getElementById('name').value;
    let family_name = document.getElementById('family_name').value;
    let phone = document.getElementById('phone').value;
    let address = document.getElementById('address').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
            username:username,
            name: name,
            family_name : family_name,
            phone : phone,
            address : address,
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

password_check = () => {
    let password = $('#password').val();
    let retype = $('#retype').val();
    if (password === retype){
        $('#div_password').css('background-color', 'green');
    }else{
        $('#div_password').css('background-color', 'red');
    }
};