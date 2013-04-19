<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li class="active">Users</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-group'></i> Users</h2>

                    <div class='pull-right'>
                        <a href='new-user.php' class='btn btn-primary'><i class='icon-file'></i> New User</a>
                    </div>
                </div>

                <? include 'help.php' ?>

                <div class='body'>
                    <div class='pull-right'>
                        <div class="input-append">
                            <input type='text' name="s" placeholder="Type your users">
                            <button class="btn" type="button"><i class='icon-search'></i></button>
                        </div>
                    </div>

                    <table class='table'>
                        <thead>
                            <th><a href="#">#</a></th>
                            <th><a href="#">Name <i class='icon-caret-down'></i></a></th>
                            <th><a href="#">Email <i class='icon-caret-up'></i></a></th>
                            <th><a href="#">Actions</a></th>
                        </thead>
                        <tbody>
                            <tr>
                                <td><a href="#">1</a></td>
                                <td>Moacir Moda Neto</td>
                                <td>modamo@paho.org</td>
                                <td>
                                    <a href="#" class='btn btn-mini'><i class='icon-pencil'></i></a>
                                    <a href="#" class='btn btn-mini'><i class='icon-remove'></i></a>
                                </td>
                            </tr>
                            <tr>
                                <td><a href="#">1</a></td>
                                <td>Moacir Moda Neto</td>
                                <td>modamo@paho.org</td>
                                <td>
                                    <a href="#" class='btn btn-mini'><i class='icon-pencil'></i></a>
                                    <a href="#" class='btn btn-mini'><i class='icon-remove'></i></a>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <? include 'pagination.php' ?>              
                </div>                
            </div>
            <? include 'footer.php' ?>
        </div>
    </body>
</html>