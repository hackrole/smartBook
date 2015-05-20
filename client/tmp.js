function iter(node, lt){
  $.each(node, function(k, v){
    if(v.children){
      lt.append([v.title, v.id]);
      iter(v.children, lt);
    }
  });
}
