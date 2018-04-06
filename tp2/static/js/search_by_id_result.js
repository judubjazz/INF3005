send_email = () => {
    let url = 'http://localhost:5000/send_email';
    let email = document.getElementById('email').value;
    let message = document.getElementById('message').value;
    let animal_id=document.getElementById('animal_id').innerHTML;

    const requestOptions = {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            email: email,
            message: message,
            animal_id:animal_id,
        })
    };

    fetch(url, requestOptions)
        .then(res =>res.json())
        .catch(err=>{
            console.log("error :" + err)
        })
        .then(res=>{
            console.log(res);
            if (res.success){
                $('#response').html('a email has been sent to the owner, please remember! adopting an animal is a full life contract.')
            }else{
                alert(res.error);
            }
        })
};