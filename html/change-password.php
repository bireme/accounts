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
                <li class="active">Change Password</li>
            </ul>
            

            <div class="container-fluid content main">
                <!--  header -->
                <div class='header'>
                    <h2><i class='icon-globe'></i> Change Password</h2>
                </div>

                <? include 'help.php' ?>

                <div class='body'>
                    <form>
                        <fieldset>                                
                            <div class='field'>
                                <label for="field">Old password</label>
                                <input type='password'>
                            </div>

                            <div class='field'>
                                <label for="field">New password</label>
                                <input type='password'>
                            </div>

                            <div class='field'>
                                <label for="field">Confirm password</label>
                                <input type='password'>
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