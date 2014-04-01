$(document).ready(function (){
	
	$("#headerContent a").tooltip();

$("#signup").submit(function (event)
{
	var a=$("#name");
	if(!(a.val().match(/^[a-zA-Z ]+$/)))
	{
		alert("Please enter a valid name");
		a.focus();
		return false;
	}
	var a=$("#phone");
	if(!(a.val().match(/^[789]\d{9}$/)))
	{
		alert("Please enter a valid phone number");
		a.focus();
		return false;
	}
	var a=$("#password");
	var b=$("#confirm_password");
	if( a.val()=="" ){
		alert("Please enter a valid password");
		a.focus();
		return false;
	}
	if(!a.val()==b.val()){
		alert("Password Mismatch !!");
		a.focus();
		return false;
	}
});

});


function coverUp(){
	$("#cover").fadeOut();
}