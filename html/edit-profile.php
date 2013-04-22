<!DOCTYPE html>
<html>
    <? include 'head.php' ?>
    <body>
        <div class='mask'><img src='static/image/loading.gif'></div>
        <div class="wrap">
            <? include 'menu.php' ?>

            
            <ul class="breadcrumb">
                <li><a href="#">Home</a> <span class="divider">/</span></li>
                <li><a href="#">User</a><span class="divider">/</span></li>
                <li class="active">Edit Your Profile</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-globe'></i> Edit Your Profile <small>(normal user)</small></h2>

                    <div class='pull-right'>
                        <a href='#' class='btn'>Change Password</a>
                    </div>
                </div>

                <? include 'help.php' ?>

                <div class='body'>
                    <form>
                        <fieldset>                                
                            <div class='field'>
                                <label for="field">Name</label>
                                <input type='text'>
                            </div>
                            
                            <div class='field'>
                                <label for="field">Email</label>
                                <input type='text'>
                            </div>
                        </fieldset>

                        <div class="control-panel form-submit">
                            <button class="btn btn-primary btn-large">Submit</button>
                        </div>
                    </form>
                </div>                
            </div>
            <? include 'footer.php' ?>
        </div>
    </body>
</html>