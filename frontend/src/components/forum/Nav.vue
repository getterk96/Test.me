<template>
  <nav class="navbar navbar-default" role="navigation">
    <div class="navbar-header">
      <a rel="nofollow" class="navbar-brand" href="#">Test.Me</a>
    </div>
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav navbar-right">
        <li class="dropdown">
          <a rel="nofollow" href="#" class="dropdown-toggle" data-toggle="dropdown">个人中心<strong class="caret"></strong></a>
          <ul class="dropdown-menu">
            <li>
              <a rel="nofollow" href="#">我的主页</a>
            </li>
            <li class="divider">
            </li>
            <li>
              <a rel="nofollow" href="#">Logout</a>
            </li>
          </ul>
        </li>
      </ul>
      <form class="navbar-form navbar-right" role="search">
        <div class="form-group">
          <input class="form-control" type="text"/>
        </div>
        <button type="submit" class="btn btn-default">搜索帖子</button>
      </form>
    </div>
  </nav>
</template>

<script>
  export default {
    name: 'common-nav'
  }
</script>
