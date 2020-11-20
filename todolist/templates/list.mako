<%inherit file="common.mako"/>


<div class="box">

    <div class="box" id="heading">
        ${listName}
    </div>

    % for i in res:
      <form action="/markComplete" method="post">
        <p class="${i.completed and 'completed' or ''}">
            <input type="checkbox" name="completed" onChange="this.form.submit()" ${i.completed and 'checked' or ''}>
            <span>${i.item_text}</span>
            <span>${i.completed and 'completed' or ''}</span>
        </p>
        <input type="hidden" name="itemId" value="${i.id}"/>
      </form>
    % endfor
  <form class="item" action="/addItem" method="post">
    <input type="text" name="newItem" placeholder="New Item" autocomplete="off">
    <button class="btn1" type="submit" name="list" >+</button>
  </form>

  <form action="/delete" method="post">
    <button class="btn2" type="submit" >Clear Marked</button>
  </form>
</div>
