const usernameField=document.querySelector('#usernameField');
const feedBackArea=document.querySelector('.invalid_feedback');
const emailField=document.querySelector('#emailField');
const passwordField=document.querySelector('#passwordField');
const emailfeedBackArea=document.querySelector('.emailinvalid_feedback');
const showbutton=document.querySelector('#showbtn');
const submitbtn=document.querySelector('.submit-btn')

usernameField.addEventListener("keyup",(e)=>{
     console.log('7777777777',7777777);
     const usernameVal=e.target.value;
        usernameField.classList.remove("is-invalid");
        feedBackArea.style.display='none'; 

     if (usernameVal.length>0){

     fetch('/authentication/validate-username',{  
     body:JSON.stringify({username:usernameVal}),
     method:'POST',
     

     }).then((response)=>response.json())
     .then((data)=>{
        console.log("data",data);
        if (data.username_error){
            submitbtn.setAttribute('disabled','disabled');
            usernameField.classList.add("is-invalid");
            feedBackArea.style.display='block';
            feedBackArea.innerHTML=`<p> ${data.username_error   }<\p>`
             
        }else{
            submitbtn.removeAttribute('disabled');
        }

     })
    };
});

emailField.addEventListener('keyup',(e)=>{
    console.log('7777777777',7777777);
     const emailVal=e.target.value;
        emailField.classList.remove("is-invalid");
        emailfeedBackArea.style.display='none'; 

     if (emailVal.length>0){

     fetch('/authentication/validate-email',{  
     body:JSON.stringify({email:emailVal}),
     method:'POST',
     

     }).then((response)=>response.json())
     .then((data)=>{
        console.log("data",data);
        if (data.email_error){
            submitbtn.setAttribute('disabled','disabled');
            emailField.classList.add("is-invalid");
            emailfeedBackArea.style.display='block';
            emailfeedBackArea.innerHTML=`<p> ${data.email_error   }<\p>`
             
        }else{
            submitbtn.removeAttribute('disabled');
        }

     })
    };
})
const handleToggleInput=(e)=>{
    if(showbutton.textContent=='SHOW'){
        showbutton.textContent='HIDE';
        passwordField.setAttribute('type','text')
    }else{
        showbutton.textContent='SHOW';
        passwordField.setAttribute('type','password')
    }
}
showbutton.addEventListener('click',handleToggleInput);