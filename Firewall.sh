#a regra a seguir restringe o acesso externo de todos os endereços IP, exceto do ip interno da vm

iptables -I DOCKER-USER -i ext_if ! -s 10.158.0.2 -j DROP
iptables -I DOCKER-USER -p tcp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT


iptables -A INPUT -p tcp -m tcp -m multiport ! --dports 80,443,3306 -j DROP
iptables -A INPUT -p tcp -m tcp -m multiport --dports 80,443,3306 -j ACCEPT
<insert further allowed list here>
iptables -A INPUT -m conntrack -j ACCEPT  --ctstate RELATED,ESTABLISHED
iptables -A INPUT -j DROP
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -j DROP
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -j DROP