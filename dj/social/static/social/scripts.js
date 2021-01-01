// javascript.js

canvas               = O('logo')
context              = canvas.getContext('2d')
context.font         = 'bold italic 97px Georgia'
context.textBaseline = 'top'
image                = new Image()
image.src            = '/static/social/robin.gif'

image.onload = function()
{
  gradient = context.createLinearGradient(0, 0, 0, 89)
  gradient.addColorStop(0.00, '#faa')
  gradient.addColorStop(0.66, '#f00')
  context.fillStyle = gradient
  context.fillText(  "R  bin's Nest", 0, 0)
  context.strokeText("R  bin's Nest", 0, 0)
  context.drawImage(image, 64, 32)
}

function O(i)
{
  if (typeof i == 'object') return i
  else return document.getElementById(i)
}

function S(i)
{
  return O(i).style
}

function C(n)
{
  var t = document.getElementsByTagName('*')
  var o = []

  for (var i in t)
  {
    var e = typeof t[i] == 'object' ? t[i].className : ''
    
    if (e                        ==  n ||
        e.indexOf(' ' + n + ' ') != -1 ||
        e.indexOf(      n + ' ') ==  0 ||
        e.indexOf(' ' + n      ) == (e.length - n.length - 1))
          o.push(t[i])
  }
  return o
}

function checkUser(user)
{
  if (user.value == '')
  {
    O('info').innerHTML = ''
    return
  }

  params  = "user=" + user.value
  request = new ajaxRequest()
  request.open("POST", "/social/checkuser/", true)
  request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
  // request.setRequestHeader("Content-length", params.length)
  // request.setRequestHeader("Connection", "close")

  request.onreadystatechange = function()
  {
    if (this.readyState == 4)
      if (this.status == 200)
        if (this.responseText != null)
          O('info').innerHTML = this.responseText
  }
  request.send(params)
}

function ajaxRequest()
{
  try { var request = new XMLHttpRequest() }
  catch(e1) {
    try { request = new ActiveXObject("Msxml2.XMLHTTP") }
    catch(e2) {
      try { request = new ActiveXObject("Microsoft.XMLHTTP") }
      catch(e3) {
        request = false
  } } }
  return request
}

// Search function
function searchUser(user)
{
  if (user.value == '')
  {
    O('info').innerHTML = ''
    return
  }

  params  = "user=" + user.value
  request = new ajaxRequest()
  request.open("POST", "/social/search/", true)
  request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
  // request.setRequestHeader("Content-length", params.length)
  // request.setRequestHeader("Connection", "close")

  request.onreadystatechange = function()
  {
    if (this.readyState == 4)
      if (this.status == 200)
        if (this.responseText != null)
          O('info').innerHTML = this.responseText
  }
  request.send(params)
}

// Validation for Login and Signup
function signUpvalidateForm() {
    var x = document.forms["signupForm"]["user"].value;
    var username = document.forms["signupForm"]["user"].value;
    var ck_username = /^[A-Za-z0-9_]{1,20}$/;
    var ck_password = /^[A-Za-z0-9!@#$%^&*()_]{6,20}$/;
    console.log(x)
    if (!ck_username.test(x)){
        swal("Invalid username!")
        return false
    }

    var x = document.forms["signupForm"]["pass"].value;
    if (!ck_password.test(x)) {
        swal("Invalid password!")
        return false
    }
}

// Perfect Username and Password Validation
function loginValidateForm() {
    var x = document.forms["loginForm"]["username"].value;
    var ck_username = /^[A-Za-z0-9_]{1,20}$/;
    var ck_password = /^[A-Za-z0-9!@#$%^&*()_]{6,20}$/;
    console.log(x)
    if (!ck_username.test(x)){
        swal("Invalid username!")
        return false
    }

    var x = document.forms["loginForm"]["password"].value;
    if (!ck_password.test(x)) {
        swal("Invalid password!")
        return false
    }
}
