document.addEventListener('DOMContentLoaded',()=>{
    var elems = document.querySelectorAll('select');
    var options = document.querySelectorAll('options')
    var instances = M.FormSelect.init(elems, options);

    const myButton = document.getElementById('myButton');
    if(myButton) myButton.addEventListener('click', ()=>{
        alert('Click button')
    })
})