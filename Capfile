require 'rubygems'
require 'railsless-deploy'

set :application, "air-toxics"
set :repository,  "git://github.com/drcs/myairsample.org.git"
set :scm,         :git
set :user,        "gbenison"
set :use_sudo,    false
set :branch,      "release/production"
set :deploy_to,   "/home/gbenison/gwenomatic/production"

# Reference: http://stackoverflow.com/questions/3023857/capistrano-and-deployment-of-a-website-from-github
set :normalize_asset_timestamps, false

role :web,        "cameronbridge.dreamhost.com"

load 'deploy' if respond_to?(:namespace) # cap2 differentiator

namespace :deploy do
  task :restart do
  end
end
