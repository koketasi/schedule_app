const edit_func=(rowid)=>{
    const card=document.getElementById(rowid);
    card.querySelector('.view').style.display='none';
    card.querySelector('.edit').style.display='block';
}
const view_func=(rowid)=>{
    const card=document.getElementById(rowid);
    card.querySelector('.edit').style.display='none';
    card.querySelector('.view').style.display='block';
}