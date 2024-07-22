function deleteBlog(id){
    if(confirm("Are you sure you want to delete this blog post?")){
        location.href = id+'/delete/';
    }
}