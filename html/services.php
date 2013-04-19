<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li class="active">Services</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-star'></i> Services</h2>

                    <div class='pull-right'>
                        <a href='new-service.php' class='btn btn-primary'><i class='icon-file'></i> New Service</a>
                    </div>
                </div>

                <? include 'help.php' ?>

                <div class='body'>
                    <div class='pull-right'>
                        <div class="input-append">
                            <input type='text' name="s" placeholder="Type your services">
                            <button class="btn" type="button"><i class='icon-search'></i></button>
                        </div>
                    </div>

                    <table class='table'>
                        <thead>
                            <th><a href="#">#</a></th>
                            <th><a href="#">Name <i class='icon-caret-down'></i></a></th>
                            <th><a href="#">Acronym <i class='icon-caret-up'></i></a></th>
                            <th><a href="#">Actions</a></th>
                        </thead>
                        <tbody>
                            <tr>
                                <td><a href="#">1</a></td>
                                <td>Diretório de Eventos</td>
                                <td>DIREVE</td>
                                <td>
                                    <a href="#" class='btn btn-mini'><i class='icon-pencil'></i></a>
                                    <a href="#" class='btn btn-mini'><i class='icon-remove'></i></a>
                                </td>
                            </tr>
                            <tr>
                                <td><a href="#">1</a></td>
                                <td>Diretório de Eventos</td>
                                <td>DIREVE</td>
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