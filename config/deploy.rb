set :application, "air-toxics"
set :repository,  "git://github.com/gbenison/gwenomatic.git"
set :deploy_to,   "/home/gbenison/air-toxics.com"

set :scm, :git
set :user, "gbenison"
set :use_sudo, false

role :web, "watanabe.dreamhost.com"

# if you're still using the script/reaper helper you will need
# these http://github.com/rails/irs_process_scripts

# If you are using Passenger mod_rails uncomment this:
# namespace :deploy do
#   task :start do ; end
#   task :stop do ; end
#   task :restart, :roles => :app, :except => { :no_release => true } do
#     run "#{try_sudo} touch #{File.join(current_path,'tmp','restart.txt')}"
#   end
# end
