require 'twitter'
require 'yaml'
require 'csv'

keys = YAML.load_file('keys.yml')

client = Twitter::REST::Client.new do |config|
  config.consumer_key      = keys["CONSUMER_KEY"]
  config.consumer_secret   = keys["CONSUMER_SECRET"]
end

def collect_with_max_id(collection=[], max_id=nil, &block)
  response = yield(max_id)
  collection += response
  response.empty? ? collection.flatten : collect_with_max_id(collection, response.last.id - 1, &block)
end

def client.get_all_tweets(user)
  collect_with_max_id do |max_id|
    options = {count: 200, include_rts: true}
    options[:max_id] = max_id unless max_id.nil?
    user_timeline(user, options)
  end
end

tweets = []
users = ['BarackObama', 'govchristie']

users.each do |user|
  tweets += client.get_all_tweets(user)
end

CSV.open("tweets.csv", "w") do |csv|
  tweets.each do |tweet|
    csv << [tweet.text, tweet.user.screen_name]
  end
end