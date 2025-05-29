#!/bin/bash
# 🔐 Restore SSH keys from raw Replit secrets

mkdir -p ~/.ssh

# Directly write private/public keys as raw text
echo "$PRIVATE_SSH_KEY" > ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519

echo "$PUBLIC_SSH_KEY" > ~/.ssh/id_ed25519.pub
chmod 644 ~/.ssh/id_ed25519.pub

# Launch SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Verify connection
ssh -T git@github.com

echo "✅ SSH key restored and GitHub connection attempted."