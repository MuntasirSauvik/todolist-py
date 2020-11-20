<%inherit file="common.mako"/>

<div class="box" id="heading">

</div>

<div class="box">

  <form class="item" action="/addItem" method="post">
    <input type="text" name="newItem" placeholder="New Item" autocomplete="off">
    <button class="btn1" type="submit" name="list" >+</button>
  </form>

  <form action="/delete" method="post">
    <button class="btn2" type="submit" >Clear Marked</button>
  </form>
</div>
