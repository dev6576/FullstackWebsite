const searchField=document.querySelector('#searchField');
const tableOutput=document.querySelector(".table-output");
const AppTable=document.querySelector(".app-table");
const tableBody=document.querySelector(".table-body")
tableOutput.style.display="none";

searchField.addEventListener('keyup',(e)=>{
    const searchValue=e.target.value

    if(searchValue.trim().length>0){
    tableBody.innerHTML=''
    fetch('/search-expenses',{  
        body:JSON.stringify({searchText:searchValue}),
        method:'POST',
        }).then((response)=>response.json())
        .then((data)=>{
           console.log(data);
           AppTable.style.display='none'
           tableOutput.style.display="block";
           if(data.length==0){
                tableOutput.innerHTML="No results found"
           }else{
            data.forEach(item=>{
                tableBody.innerHTML+=`
                <tr>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                <td>${item.amount}</td>
                </tr>
                `
            })
           

           }
        })
    }else{
        AppTable.style.display='block'
        tableOutput.style.display='none'
    }
    

})