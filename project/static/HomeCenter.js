/**
 * Created by Peter on 22.01.2016.
 */

$("input:radio[name=selection]").change(function(){
    var id = $(this).attr('id')
    console.log(id);
    var title = $("label[for="+id+"]").html();
    console.log(title);
    $("input:hidden[name=title]").val(title);
});