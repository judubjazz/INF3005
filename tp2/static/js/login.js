login = () => {
    let url = "http://localhost:5000/login";
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
        const requestOptions = {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    };

    fetch(url, requestOptions)
        .then(res =>res.json())
        .catch(err=>{console.log("error :" + err)})
        .then(res => {
            console.log(res);
            if (res.success){
                window.location=res.url;
            }else{
                //TODO append div for error
                $('#login_error').html(res.error);
            }
        });
};

forgot_password = () => {
    window.location = 'http://localhost:5000/password_recovery'
};



