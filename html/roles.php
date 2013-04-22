<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li class="active">Roles</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-lock'></i> Roles</h2>

                    <div class='pull-right'>
                        <a href='new-role.php' class='btn btn-primary'><i class='icon-file'></i> New Role</a>
                    </div>
                </div>

                <? include 'help.php' ?>

                <div class='body'>
                    <table class='table'>
                        <thead>
                            <th><a href="#">#</a></th>
                            <th><a href="#">Name <i class='icon-caret-down'></i></a></th>
                            <th><a href="#">Acronym <i class='icon-caret-down'></i></a></th>
                            <th><a href="#">Actions</a></th>
                        </thead>
                        <tbody>
                            <tr>
                                <td><a href="#">1</a></td>
                                <td>Documentalist</td>
                                <td>doc</td>
                                <td><a href="#" class='btn btn-mini'><i class='icon-remove'></i></a></td>
                            </tr>
                            <tr>
                                <td><a href="#">1</a></td>
                                <td>Editor</td>
                                <td>edi</td>
                                <td><a href="#" class='btn btn-mini'><i class='icon-remove'></i></a></td>
                            </tr>
                            <tr>
                                <td><a href="#">1</a></td>
                                <td>Adiministrator</td>
                                <td>adm</td>
                                <td><a href="#" class='btn btn-mini'><i class='icon-remove'></i></a></td>
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