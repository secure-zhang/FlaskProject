//注意：导航 依赖 element 模块，否则无法进行功能性操作

layui.use('element', function(){
  var element = layui.element;

  //…
});
//Demo
layui.use('form', function(){
  var form = layui.form;

  //监听提交
  form.on('submit(formDemo)', function(data){
    layer.msg(JSON.stringify(data.field));
    return false;
  });
});
