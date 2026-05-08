
console.log("Static file loaded!")
document.addEventListener('DOMContentLoaded',()=>{
    const myButton = document.getElementById('myButton');
    if(myButton) myButton.addEventListener('click', ()=>{
        alert('Click button')
    })
})